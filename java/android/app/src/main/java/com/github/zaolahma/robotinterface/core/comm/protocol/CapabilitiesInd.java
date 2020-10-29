package com.github.zaolahma.robotinterface.core.comm.protocol;

import java.util.ArrayList;
import java.util.List;

public class CapabilitiesInd implements Message {
    public static final int S_MESSAGE_ID = 3;

    private List<Byte> mCapabilities;

    public CapabilitiesInd() {
        mCapabilities = new ArrayList<Byte>();
    }

    public void addCapability(Byte capability) {
        mCapabilities.add(capability);
    }

    @Override
    public byte[] encode() {
        byte[] retVal = new byte[mCapabilities.size()];

        for (int i = 0; i < mCapabilities.size(); ++i) {
            retVal[i] = mCapabilities.get(i);
        }

        return retVal;
    }

    @Override
    public void decode(byte[] toDecode) {
        mCapabilities = new ArrayList<Byte>();
        for (int i = 0; i < toDecode.length; ++i) {
            mCapabilities.add(toDecode[i]);
        }
    }

    @Override
    public byte getMessageId() {
        return CapabilitiesInd.S_MESSAGE_ID;
    }
}
