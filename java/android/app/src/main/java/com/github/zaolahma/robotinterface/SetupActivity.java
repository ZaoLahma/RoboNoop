package com.github.zaolahma.robotinterface;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.github.zaolahma.robotinterface.core.comm.NetworkContext;
import com.github.zaolahma.robotinterface.core.comm.NetworkThread;
import com.github.zaolahma.robotinterface.core.comm.protocol.MessageProtocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.Protocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.SonarDataMessage;
import com.github.zaolahma.robotinterface.ui.shared.AppContext;
import com.google.android.material.textfield.TextInputEditText;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SetupActivity extends AppCompatActivity implements View.OnClickListener {
    private static final int S_CONN_AGGREGATOR_PORT_NO = 3306;
    private TextInputEditText mRobotAddress;
    private Button mConnectButton;

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

        mConnectButton.setOnClickListener(this);

        System.out.println("On create called");
    }

    @Override
    public void onClick(View v) {
        final String robotAddress = mRobotAddress.getText().toString();
        Map<Integer, Class> classDefinitions = new HashMap<Integer, Class>();
        classDefinitions.put(SonarDataMessage.MESSAGE_ID, SonarDataMessage.class);
        MessageProtocol messageProtocol = new MessageProtocol(classDefinitions);
        List<Protocol> protocolList = new ArrayList<Protocol>();
        protocolList.add(messageProtocol);
        NetworkThread nwThread =
                new NetworkThread(getApplicationContext(),
                        robotAddress,
                        S_CONN_AGGREGATOR_PORT_NO,
                        protocolList);
        nwThread.start();

        while (!nwThread.isStarted())
        {
            //Do nothing
        }
        if (nwThread.isRunning()) {
            NetworkContext.getApi().setNetworkThread(nwThread);

            Intent intent = new Intent(this, MainActivity.class);
            startActivity(intent);
        } else {
            System.out.println("Failed to connect!");
        }
    }
}