package com.github.zaolahma.robotinterface.ui.workspace;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.github.zaolahma.robotinterface.R;
import com.github.zaolahma.robotinterface.core.comm.NetworkThread;
import com.github.zaolahma.robotinterface.core.comm.protocol.MessageProtocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.Protocol;
import com.github.zaolahma.robotinterface.core.comm.protocol.SonarDataMessage;
import com.github.zaolahma.robotinterface.ui.workspace.core.WorkspaceBase;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class NetworkWorkspace extends WorkspaceBase implements View.OnClickListener {
    NetworkThread mNetworkThread;

    @Override
    public String getWorkspaceName() {
        return "Network";
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.network_workspace, container, false);
        Button button = (Button) root.findViewById(R.id.nw_connect_button);
        button.setOnClickListener(this);
        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        if (null != mNetworkThread) {
            mNetworkThread.exit();
        }
    }

    @Override
    public void onClick(View v) {
        System.out.println("Connect!");
        Map<Integer, Class> classDefinitions = new HashMap<Integer, Class>();
        classDefinitions.put(SonarDataMessage.MESSAGE_ID, SonarDataMessage.class);
        MessageProtocol messageProtocol = new MessageProtocol(classDefinitions);
        List<Protocol> protocolList = new ArrayList<Protocol>();
        protocolList.add(messageProtocol);
        mNetworkThread = new NetworkThread(getContext(), "192.168.0.44", 3300, protocolList);
        mNetworkThread.start();
    }
}
