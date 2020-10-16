package com.github.zaolahma.robotinterface.core.comm.protocol;

import androidx.annotation.NonNull;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class SonarDataMessage implements Message {
    public static final int MESSAGE_ID = 200;

    private int mDistance;

    @Override
    public byte[] encode() {
        return null;
    }

    @Override
    public void decode(byte[] toDecode) {
        ByteBuffer headerData = ByteBuffer.wrap(toDecode);
        headerData.order(ByteOrder.BIG_ENDIAN);
        short tmp = headerData.getShort();
        mDistance = tmp >= 0 ? tmp : 0x10000 + tmp;
    }

    public int getDistance() {
        return mDistance;
    }

    @NonNull
    @Override
    public String toString() {
        return "mDistance: " + mDistance;
    }
}
