package com.github.zaolahma.robotinterface.core.comm.protocol;

public class UnlockInd implements Message {
    public static final byte S_MESSAGE_ID = 10;

    @Override
    public byte[] encode() {
        return null;
    }

    @Override
    public void decode(byte[] toDecode) {
        /*
        Intentionally left empty
         */
    }

    @Override
    public byte getMessageId() {
        return S_MESSAGE_ID;
    }
}
