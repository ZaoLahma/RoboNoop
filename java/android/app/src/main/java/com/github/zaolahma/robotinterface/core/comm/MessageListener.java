package com.github.zaolahma.robotinterface.core.comm;

import com.github.zaolahma.robotinterface.core.comm.protocol.Message;

public interface MessageListener {
    void handleMessage(Message message);
}
