package com.github.zaolahma.robotinterface.core.comm.protocol;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class MoveInd implements Message {
    public static final int S_MESSAGE_ID = 12;

    public static final Map<String, Short> S_DIRECTION;
    static {
        Map<String, Short> directionMap = new HashMap<String, Short>();
        directionMap.put("STOP", (short) 0);
        directionMap.put("FORWARD", (short) 1);
        directionMap.put("LEFT", (short) 2);
        directionMap.put("RIGHT", (short) 3);
        directionMap.put("BACKWARD", (short) 4);
        S_DIRECTION = Collections.unmodifiableMap(directionMap);
    }

    private short mDirection;
    private short mPower;
    private short mSubsystem;

    private MoveInd() {}

    public MoveInd(short direction, short power, short subsystem) {
        mDirection = direction;
        mPower = power;
        mSubsystem = subsystem;
    }

    @Override
    public byte[] encode() {
        byte[] encoded = new byte[6];

        ByteBuffer toEncode = ByteBuffer.wrap(encoded);
        toEncode.order(ByteOrder.BIG_ENDIAN);

        toEncode.putShort(mDirection);
        toEncode.putShort(mPower);
        toEncode.putShort(mSubsystem);

        return encoded;
    }

    @Override
    public void decode(byte[] toDecode) {
        /*
        Intentionally left empty
         */
    }

    @Override
    public int getMessageId() {
        return S_MESSAGE_ID;
    }
}
