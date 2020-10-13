package com.github.zaolahma.robotinterface.ui.main;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.github.zaolahma.robotinterface.R;

public class NetworkWorkspace extends WorkspaceBase implements View.OnClickListener {
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
    public void onClick(View v) {
        System.out.println("Connect!");
    }
}
