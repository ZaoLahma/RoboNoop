package com.github.zaolahma.robotinterface.core.comm;

import com.github.zaolahma.robotinterface.core.comm.protocol.Message;

import java.util.AbstractSequentialList;
import java.util.ArrayList;
import java.util.List;

public class NetworkContext {
    private static NetworkContext S_INSTANCE = null;
    private NetworkThread mNetworkThread;
    private List<MessageListener> mMessageListeners;
    private Message mMessageToSend;

    private NetworkContext() {
        mMessageListeners = new ArrayList<MessageListener>();
    }

    public static NetworkContext getApi() {
        if (null == S_INSTANCE) {
            S_INSTANCE = new NetworkContext();
        }
        return S_INSTANCE;
    }

    public void setNetworkThread(NetworkThread networkThread) {
        if (null != mNetworkThread) {
            mNetworkThread.exit();
        }
        mNetworkThread = networkThread;
    }

    public void sendMessage(Message message) {
        mMessageToSend = message;
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
        mNetworkThread.exit();
    }
}
