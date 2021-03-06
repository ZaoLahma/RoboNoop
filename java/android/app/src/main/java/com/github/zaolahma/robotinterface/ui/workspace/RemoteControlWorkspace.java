package com.github.zaolahma.robotinterface.ui.workspace;

import android.hardware.SensorManager;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.github.zaolahma.robotinterface.R;
import com.github.zaolahma.robotinterface.core.comm.NetworkContext;
import com.github.zaolahma.robotinterface.core.comm.NetworkThread;
import com.github.zaolahma.robotinterface.core.comm.protocol.Message;
import com.github.zaolahma.robotinterface.core.comm.protocol.MoveInd;
import com.github.zaolahma.robotinterface.core.comm.protocol.Protocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.UnlockInd;
import com.github.zaolahma.robotinterface.ui.control.GyroControl;
import com.github.zaolahma.robotinterface.ui.workspace.core.WorkspaceBase;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class RemoteControlWorkspace extends WorkspaceBase implements View.OnClickListener {
    private final SensorManager mSensorManager;
    private SensorDataThread mSensorDataThread;

    public RemoteControlWorkspace(SensorManager sensorManager) {
        mSensorManager = sensorManager;
    }

    @Override
    public String getWorkspaceName() {
        return "Remote control";
    }

    @Override
    public void deactivate() {
        if (null != mSensorDataThread) {
            mSensorDataThread.exit();
        }
        mSensorDataThread = null;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.remote_ctrl_workspace, container, false);
        Button button = (Button) root.findViewById(R.id.enable_button);
        button.setOnClickListener(this);
        return root;
    }

    @Override
    public void onClick(View v) {
        mSensorDataThread = new SensorDataThread(mSensorManager);
        mSensorDataThread.start();
    }

    private class SensorDataThread extends Thread {
        private static final int S_TARGET_FPS = 4;
        private static final int S_MILLIS_IN_SECOND = 1000;
        private static final short S_SUBSYSTEM = 1;
        private static final short S_POWER = 100;
        private GyroControl mGyroControl;
        private boolean mRunning;

        SensorDataThread(SensorManager sensorManager) {
            mGyroControl = new GyroControl(sensorManager);
        }

        @Override
        public void run() {
            mRunning = true;
            while (mRunning) {
                double pitchAngle = mGyroControl.getPitchAngle();
                double rollAngle = mGyroControl.getRollAngle();

                System.out.println("pitchAngle: " + pitchAngle + ", rollAngle: " + rollAngle);

                Message message = null;

                if (Math.abs(pitchAngle) >= Math.abs(rollAngle)) {
                    if (pitchAngle >= 30.0) {
                        System.out.println("Forward");
                        message = new MoveInd(MoveInd.S_DIRECTION.get("FORWARD"), S_POWER, S_SUBSYSTEM);
                    } else if (pitchAngle <= -30.0) {
                        System.out.println("Backward");
                        message = new MoveInd(MoveInd.S_DIRECTION.get("BACKWARD"), S_POWER, S_SUBSYSTEM);
                    } else {
                        System.out.println("Stop");
                        message = new MoveInd(MoveInd.S_DIRECTION.get("STOP"), S_POWER, S_SUBSYSTEM);
                    }
                } else {
                    if (rollAngle >= 30.0) {
                        System.out.println("Left");
                        message = new MoveInd(MoveInd.S_DIRECTION.get("LEFT"), S_POWER, S_SUBSYSTEM);
                    } else if (rollAngle <= -30.0) {
                        System.out.println("Right");
                        message = new MoveInd(MoveInd.S_DIRECTION.get("RIGHT"), S_POWER, S_SUBSYSTEM);
                    } else {
                        System.out.println("Stop");
                        message = new MoveInd(MoveInd.S_DIRECTION.get("STOP"), S_POWER, S_SUBSYSTEM);
                    }
                }

                UnlockInd unlockMessage = new UnlockInd();
                try {
                    NetworkContext.getApi().sendMessage(unlockMessage);
                    NetworkContext.getApi().sendMessage(message);
                } catch (IOException e) {
                    mRunning = false;
                    this.interrupt();
                }

                if (mRunning) {
                    long toSleep = S_MILLIS_IN_SECOND / S_TARGET_FPS;
                    try {
                        Thread.sleep(toSleep);
                    } catch (InterruptedException e) {
                        mRunning = false;
                    }
                }
            }
        }

        public void exit() {
            this.interrupt();
            mRunning = false;
        }
    }
}
