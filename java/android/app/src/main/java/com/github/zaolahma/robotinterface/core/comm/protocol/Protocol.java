package com.github.zaolahma.robotinterface.core.comm.protocol;

public interface Protocol {
    public Message decode(byte[] data);
}
