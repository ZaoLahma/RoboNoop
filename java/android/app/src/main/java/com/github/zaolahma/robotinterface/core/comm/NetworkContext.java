package com.github.zaolahma.robotinterface.core.comm;

import com.github.zaolahma.robotinterface.core.comm.protocol.Message;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class NetworkContext {
    private static NetworkContext S_INSTANCE = null;
    private static NetworkThread mNetworkRxThread;
    private static NetworkTxThread mNetworkTxThread;
    private List<MessageListener> mMessageListeners;
    private List<NetworkStateListener> mNetworkStateListeners;

    private NetworkContext() {
        mMessageListeners = new ArrayList<MessageListener>();
        mNetworkStateListeners = new ArrayList<NetworkStateListener>();
    }

    public static NetworkContext getApi() {
        if (null == S_INSTANCE) {
            S_INSTANCE = new NetworkContext();
        }
        return S_INSTANCE;
    }

    public void registerNetworkStateListener(NetworkStateListener listener) {
        if (!mNetworkStateListeners.contains(listener)) {
            mNetworkStateListeners.add(listener);
        }
    }

    public void onConnect() {
        for (NetworkStateListener listener : mNetworkStateListeners) {
            listener.onConnected();
        }
    }

    public void setNetworkThread(NetworkThread networkThread) {
        if (null != mNetworkRxThread) {
            mNetworkRxThread.exit();
        }
        if (null != mNetworkTxThread) {
            mNetworkTxThread.exit();
        }
        mNetworkTxThread = new NetworkTxThread();
        mNetworkTxThread.start();

        mNetworkRxThread = networkThread;
    }

    public void sendMessage(Message message) throws IOException {
        mNetworkTxThread.queueMessage(message);
    }

    public void receiveMessage(Message message) {
        for (MessageListener listener : mMessageListeners) {
            listener.handleMessage(message);
        }
    }

    public void addMessageListener(MessageListener messageListener) {
        mMessageListeners.add(messageListener);
    }

    public void disconnect() {
        if (null != mNetworkRxThread) {
            mNetworkRxThread.exit();
        }

        if (null != mNetworkTxThread) {
            mNetworkTxThread.exit();
        }

        for (NetworkStateListener listener : mNetworkStateListeners) {
            listener.onDisconnected();
        }
    }

    private static class NetworkTxThread extends Thread {
        private final List<Message> mTxList = new ArrayList<Message>();
        private final Lock mTxLock = new ReentrantLock();
        private final Condition mTxCond = mTxLock.newCondition();
        private boolean mActive = false;

        public void queueMessage(Message message) {
            mTxLock.lock();
            mTxList.add(message);
            mTxCond.signal();
            mTxLock.unlock();
        }

        public void exit() {
            mActive = false;
            this.interrupt();
        }

        @Override
        public void run() {
            System.out.println("NetworkTxThread started");
            mActive = true;
            while (mActive) {
                try {
                    mTxLock.lock();
                    mTxCond.await();
                    if (null != mNetworkRxThread) {
                        for (Message message : mTxList) {
                            mNetworkRxThread.sendMessage(message);
                            System.out.println("Sending message " + message.getMessageId());
                        }
                        mTxList.clear();
                    }
                } catch (InterruptedException | IOException e) {
                    mActive = false;
                } finally {
                    mTxLock.unlock();
                }
            }
            System.out.println("NetworkTxTread exited");
        }
    }
}