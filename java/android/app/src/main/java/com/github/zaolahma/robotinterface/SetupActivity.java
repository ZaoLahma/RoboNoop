package com.github.zaolahma.robotinterface;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.graphics.Color;
import android.hardware.SensorManager;
import android.net.Network;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.github.zaolahma.robotinterface.core.comm.NetworkContext;
import com.github.zaolahma.robotinterface.core.comm.NetworkStateListener;
import com.github.zaolahma.robotinterface.core.comm.NetworkThread;
import com.github.zaolahma.robotinterface.core.comm.protocol.CapabilitiesInd;
import com.github.zaolahma.robotinterface.core.comm.protocol.DataTransferMessage;
import com.github.zaolahma.robotinterface.core.comm.protocol.Message;
import com.github.zaolahma.robotinterface.core.comm.protocol.MessageProtocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.MoveInd;
import com.github.zaolahma.robotinterface.core.comm.protocol.Protocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.SonarDataMessage;
import com.github.zaolahma.robotinterface.ui.shared.AppContext;
import com.google.android.material.textfield.TextInputEditText;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SetupActivity extends AppCompatActivity implements View.OnClickListener, NetworkStateListener {
    private static final int S_CONN_AGGREGATOR_PORT_NO = 3306;
    private TextInputEditText mRobotAddress;
    private Button mConnectButton;
    private TextView mConnectionStatus;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_setup);

        /*
        Don't rotate please
         */
        setRequestedOrientation (ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        mRobotAddress = (TextInputEditText) findViewById(R.id.robot_address);
        mConnectButton = (Button) findViewById(R.id.connect_button);
        mConnectionStatus = (TextView) findViewById(R.id.setup_connection_status);

        mConnectButton.setOnClickListener(this);

        NetworkContext.getApi().registerNetworkStateListener(this);
    }

    @Override
    public void onClick(View v) {
        final String robotAddress = mRobotAddress.getText().toString();
        Map<Byte, Class> classDefinitions = new HashMap<Byte, Class>();
        classDefinitions.put(SonarDataMessage.S_MESSAGE_ID, SonarDataMessage.class);
        classDefinitions.put(DataTransferMessage.S_MESSAGE_ID, DataTransferMessage.class);
        MessageProtocol messageProtocol = new MessageProtocol(classDefinitions);
        List<Protocol> protocolList = new ArrayList<Protocol>();
        protocolList.add(messageProtocol);
        NetworkThread nwThread =
                new NetworkThread(getApplicationContext(),
                        robotAddress,
                        S_CONN_AGGREGATOR_PORT_NO,
                        protocolList);
        nwThread.start();

        NetworkContext.getApi().setNetworkThread(nwThread);
    }

    @Override
    public void onConnected() {
        CapabilitiesInd capabilitiesInd = new CapabilitiesInd();
        capabilitiesInd.addCapability(DataTransferMessage.S_MESSAGE_ID);
        capabilitiesInd.addCapability(SonarDataMessage.S_MESSAGE_ID);
        capabilitiesInd.addCapability(MoveInd.S_MESSAGE_ID);

        try {
            NetworkContext.getApi().sendMessage(capabilitiesInd);
            mConnectionStatus.setTextColor(Color.GREEN);
            mConnectionStatus.setText("Connected");
            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void onDisconnected() {
        mConnectionStatus.setTextColor(Color.RED);
        final String robotAddress = mRobotAddress.getText().toString();
        mConnectionStatus.setText("Connection to " + robotAddress + " failed");
    }
}