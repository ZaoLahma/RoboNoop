package com.github.zaolahma.robotinterface.core.comm;

import android.net.Network;

import com.github.zaolahma.robotinterface.core.comm.protocol.Message;

import java.io.IOException;
import java.util.AbstractSequentialList;
import java.util.ArrayList;
import java.util.List;

public class NetworkContext {
    private static NetworkContext S_INSTANCE = null;
    private NetworkThread mNetworkThread;
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
        if (null != mNetworkThread) {
            mNetworkThread.exit();
        }
        mNetworkThread = networkThread;
    }

    public void sendMessage(Message message) throws IOException {
        mNetworkThread.sendMessage(message);
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
        if (null != mNetworkThread) {
            mNetworkThread.exit();
        }

        for (NetworkStateListener listener : mNetworkStateListeners) {
            listener.onDisconnected();
        }
    }
}
