package com.github.zaolahma.robotinterface.core.comm.protocol;

import java.util.Arrays;
import java.util.Map;

public class MessageProtocol implements Protocol {
    private final Map<Byte, Class> mMessageDefinitions;

    public MessageProtocol(Map<Byte, Class> messageDefinitions) {
        mMessageDefinitions = messageDefinitions;
    }

    @Override
    public Message decode(byte[] data) {
        byte msgId = data[0];

        Message message = null;

        try {
            if (mMessageDefinitions.containsKey(msgId)) {
                message = (Message) mMessageDefinitions.get(msgId).newInstance();

                byte[] toDecode = Arrays.copyOfRange(data, 1, data.length);
                message.decode(toDecode);
            } else {
                System.out.println("Not containsKey msgId: " + msgId);
            }
        } catch (IllegalAccessException | InstantiationException e) {
            e.printStackTrace();
        }
        return message;
    }

    public static byte[] encode(Message message) {
        byte[] encodedMessage = message.encode();

        int messageSize = (null != encodedMessage) ? 1 + encodedMessage.length: 1;

        byte[] encodedData = new byte[messageSize];
        encodedData[0] = (byte)message.getMessageId();

        for (int i = 1; i < encodedData.length; ++i) {
            encodedData[i] = encodedMessage[i - 1];
        }

        return encodedData;
    }
}
