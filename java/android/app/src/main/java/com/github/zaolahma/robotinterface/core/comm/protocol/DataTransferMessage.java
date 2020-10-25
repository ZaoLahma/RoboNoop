package com.github.zaolahma.robotinterface.core.comm.protocol;

import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Map;

public class DataTransferMessage implements Message {
    public static final int S_MESSAGE_ID = 2;

    private Map<String, Object> mData;

    @Override
    public byte[] encode() {
        return null;
    }

    @Override
    public void decode(byte[] toDecode) {
        System.out.println("toDecode size: " + toDecode.length);
        String jsonString = new String(toDecode);
        System.out.println("jsonString: " + jsonString);
        Gson gson = new Gson();
        mData = gson.fromJson(jsonString, Map.class);
    }

    public Map<String, Object> getData() {
        return mData;
    }

    @Override
    public int getMessageId() {
        return S_MESSAGE_ID;
    }
}
