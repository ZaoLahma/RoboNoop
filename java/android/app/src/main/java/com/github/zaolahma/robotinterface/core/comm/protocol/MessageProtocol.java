package com.github.zaolahma.robotinterface.core.comm.protocol;

import java.util.Arrays;
import java.util.Map;

public class MessageProtocol implements Protocol {
    private final Map<Integer, Class> mMessageDefinitions;

    public MessageProtocol(Map<Integer, Class> messageDefinitions) {
        mMessageDefinitions = messageDefinitions;
    }

    @Override
    public Message decode(byte[] data) {
        int msgId = data[0];
        msgId = (msgId >= 1) ? msgId : 0x100 + msgId;

        Message message = null;

        System.out.println("msgId: " + msgId);

        try {
            if (mMessageDefinitions.containsKey(msgId)) {
                message = (Message) mMessageDefinitions.get(msgId).newInstance();

                byte[] toDecode = Arrays.copyOfRange(data, 1, data.length);
                message.decode(toDecode);
            }
        } catch (IllegalAccessException | InstantiationException e) {
            e.printStackTrace();
        }
        return message;
    }
}
