package com.github.zaolahma.robotinterface.core.comm;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;

import com.github.zaolahma.robotinterface.core.comm.protocol.Message;
import com.github.zaolahma.robotinterface.core.comm.protocol.MessageProtocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.Protocol;
import com.github.zaolahma.robotinterface.ui.main.AppContext;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.List;

public class NetworkThread extends Thread {
    private final String mAddress;
    private final int mPort;
    private final List<Protocol> mProtocols;
    private final Context mContext;
    private boolean mRunning;
    Socket mSocket;
    DataOutputStream mDataOutputStream;

    public NetworkThread(Context context, String address, int port, List<Protocol> protocols) {
        mContext = context;
        mRunning = true;
        mAddress = address;
        mPort = port;
        mProtocols = protocols;
    }

    /**
     * Header:
     * data_size 2 bytes
     */
    @Override
    public void run() {
        mRunning = true;
        Handler mainThreadHandler = new Handler(Looper.getMainLooper());
        DataInputStream inputStream = null;
        try {
            mSocket = new Socket(mAddress, mPort);
            inputStream = new DataInputStream(
                    new BufferedInputStream(mSocket.getInputStream()));
            mDataOutputStream = new DataOutputStream(
                    new BufferedOutputStream(mSocket.getOutputStream()));
        } catch (IOException e) {
            e.printStackTrace();
            mRunning = false;
        }

        if (mRunning) {
            System.out.println("Connected ok");
            mainThreadHandler.post(new Runnable() {
                @Override
                public void run() {
                    System.out.println("Connected status set");
                    AppContext.getApi(mContext).setString(
                            "connection_status", "connected");
                }
            });
        }

        while (mRunning) {
            System.out.println("In running");
            byte[] header = new byte[2];
            byte[] data = null;
            boolean dataComplete = false;
            try {
                System.out.println("Waiting for message header");
                int receivedHeaderSize = inputStream.read(header, 0, 2);
                int dataSize = 0;
                if (2 == receivedHeaderSize) {
                    System.out.println("header: " + header.toString());
                    ByteBuffer headerData = ByteBuffer.wrap(header);
                    headerData.order(ByteOrder.BIG_ENDIAN);
                    short tmp = headerData.getShort();
                    dataSize = tmp >= 0 ? tmp : 0x10000 + tmp;
                    data = new byte[dataSize];
                    System.out.println("Received message size: " + dataSize);
                }

                int bytesReceived = 0;
                boolean endTransmission = false;
                while (data != null && !endTransmission) {
                    int bytesLeft = dataSize - bytesReceived;
                    int chunkSize = (4096 > bytesLeft) ? bytesLeft : 4096;
                    int currReceived = inputStream.read(data, bytesReceived, chunkSize);
                    bytesReceived += currReceived;

                    if (!mRunning || 0 > currReceived) {
                        endTransmission = true;
                        mRunning = false;
                    }

                    if (bytesReceived == dataSize) {
                        dataComplete = true;
                        endTransmission = true;
                        System.out.println("Data complete");
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
                mRunning = false;
            }

            if (mRunning && dataComplete) {
                Message message = null;
                if (null != mProtocols) {
                    for (Protocol protocol : mProtocols) {
                        message = protocol.decode(data);
                    }
                }
                if (null != message) {
                    final Message toPost = message;
                    System.out.println("Message decoded: " + message.toString());
                    mainThreadHandler.post(new Runnable() {
                        @Override
                        public void run() {
                            NetworkContext.getApi().receiveMessage(toPost);
                        }
                    });
                }
            }
        }
    }

    public void exit() {
        mRunning = false;
        this.interrupt();
        System.out.println("Exit!");
    }

    public boolean isRunning() {
        return mRunning;
    }

    public void sendMessage(Message message) {
        byte[] toSend = MessageProtocol.encode(message);

        final int dataSize = toSend.length;
        int bytesSent = 0;
        boolean endTransmission = (null == mDataOutputStream);

        if (endTransmission) {
            System.out.println("mDataOutputStream: " + mDataOutputStream);
        }

        /*
        Send header
         */
        if (!endTransmission) {
            byte[] header = new byte[2];
            ByteBuffer headerBuf = ByteBuffer.wrap(header);
            headerBuf.putShort((short) dataSize);
            try {
                mDataOutputStream.write(header, 0,header.length);
                mDataOutputStream.flush();
            } catch (IOException e) {
                e.printStackTrace();
                endTransmission = true;
                mRunning = false;
                this.interrupt();
            }
        }

        /*
        Send payload
         */
        while (!endTransmission) {
            System.out.println("Attempting to send " + dataSize + " bytes");
            try {
                int bytesLeft = dataSize - bytesSent;
                int chunkSize = (4096 > bytesLeft) ? bytesLeft : 4096;
                mDataOutputStream.write(toSend, bytesSent, chunkSize);
                mDataOutputStream.flush();
                bytesSent += chunkSize;

                if (bytesSent == dataSize) {
                    endTransmission = true;
                    System.out.println("Finished sending message");
                }
            } catch (IOException e) {
                endTransmission = true;
                mRunning = false;
                this.interrupt();
                e.printStackTrace();
            }
        }
    }
}
