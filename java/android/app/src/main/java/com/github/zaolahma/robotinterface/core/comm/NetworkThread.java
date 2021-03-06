package com.github.zaolahma.robotinterface.core.comm;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;

import com.github.zaolahma.robotinterface.core.comm.protocol.Message;
import com.github.zaolahma.robotinterface.core.comm.protocol.MessageProtocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.Protocol;

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
                    NetworkContext.getApi().onConnect();
                }
            });
        }

        while (mRunning) {
            System.out.println("Running still");
            byte[] header = new byte[4];
            byte[] data = null;
            boolean dataComplete = false;
            try {
                int receivedHeaderSize = inputStream.read(header, 0, 4);
                System.out.println("receivedHeaderSize: " + receivedHeaderSize);
                int dataSize = 0;
                if (4 == receivedHeaderSize) {
                    ByteBuffer headerData = ByteBuffer.wrap(header);
                    headerData.order(ByteOrder.BIG_ENDIAN);
                    dataSize = headerData.getInt();
                    data = new byte[dataSize];
                    System.out.println("dataSize: " + dataSize);
                } else if (0 > receivedHeaderSize) {
                    mRunning = false;
                }

                int bytesReceived = 0;
                boolean endTransmission = false;
                int numReattempts = 0;
                while (data != null && !endTransmission) {
                    int bytesLeft = dataSize - bytesReceived;
                    int chunkSize = (4096 > bytesLeft) ? bytesLeft : 4096;
                    int currReceived = inputStream.read(data, bytesReceived, chunkSize);
                    bytesReceived += currReceived;

                    if (!mRunning || 0 > currReceived) {
                        if (numReattempts > 1000) {
                            endTransmission = true;
                            mRunning = false;
                        }
                        numReattempts++;
                    }

                    if (bytesReceived == dataSize) {
                        dataComplete = true;
                        endTransmission = true;
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
                    mainThreadHandler.post(new Runnable() {
                        @Override
                        public void run() {
                            NetworkContext.getApi().receiveMessage(toPost);
                        }
                    });
                } else {
                    System.out.println("Message is null");
                }
            }
        }
        mainThreadHandler.post(new Runnable() {
            @Override
            public void run() {
                NetworkContext.getApi().disconnect();
            }
        });
    }

    public void exit() {
        mRunning = false;
        this.interrupt();
        System.out.println("Exit!");
    }

    public boolean isRunning() {
        return mRunning;
    }

    public void sendMessage(Message message) throws IOException {
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
            byte[] header = new byte[4];
            ByteBuffer headerBuf = ByteBuffer.wrap(header);
            headerBuf.order(ByteOrder.BIG_ENDIAN);
            headerBuf.putInt(dataSize);
            try {
                mDataOutputStream.write(header, 0,header.length);
                mDataOutputStream.flush();
            } catch (IOException e) {
                e.printStackTrace();
                endTransmission = true;
                mRunning = false;
                this.interrupt();
                throw e;
            }
        }

        /*
        Send payload
         */
        while (!endTransmission) {
            try {
                int bytesLeft = dataSize - bytesSent;
                int chunkSize = (4096 > bytesLeft) ? bytesLeft : 4096;
                mDataOutputStream.write(toSend, bytesSent, chunkSize);
                mDataOutputStream.flush();
                bytesSent += chunkSize;

                if (bytesSent == dataSize) {
                    endTransmission = true;
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
