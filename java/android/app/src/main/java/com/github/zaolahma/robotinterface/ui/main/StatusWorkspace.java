package com.github.zaolahma.robotinterface.ui.main;

import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.github.zaolahma.robotinterface.R;

public class StatusWorkspace extends WorkspaceBase {
    @Override
    public String getWorkspaceName() {
        return "Status";
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.status_workspace, container, false);
        final TextView connectionStatusTextView = root.findViewById(R.id.connection_status);
        connectionStatusTextView.setText(AppContext.getApi(getContext()).getString("connection_status"));
        return root;
    }
}