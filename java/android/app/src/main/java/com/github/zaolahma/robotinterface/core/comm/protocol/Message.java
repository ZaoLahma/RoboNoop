package com.github.zaolahma.robotinterface.core.comm.protocol;

/**
 * Header:
 * msg_id 1 byte
 */
public interface Message {
    byte[] encode();
    void decode(byte[] toDecode);
    byte getMessageId();
}
