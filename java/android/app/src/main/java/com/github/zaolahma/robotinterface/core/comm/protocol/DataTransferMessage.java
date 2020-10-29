package com.github.zaolahma.robotinterface.core.comm.protocol;

public class DataTransferMessage implements Message {
    public static final byte S_MESSAGE_ID = 2;

    private byte[] mData;

    @Override
    public byte[] encode() {
        return null;
    }

    @Override
    public void decode(byte[] toDecode) {
        mData = toDecode;
    }

    public byte[] getData() {
        return mData;
    }

    @Override
    public byte getMessageId() {
        return S_MESSAGE_ID;
    }
}
