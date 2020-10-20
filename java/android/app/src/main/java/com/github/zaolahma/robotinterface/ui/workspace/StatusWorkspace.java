package com.github.zaolahma.robotinterface.ui.workspace;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.github.zaolahma.robotinterface.R;
import com.github.zaolahma.robotinterface.ui.shared.AppContext;
import com.github.zaolahma.robotinterface.ui.workspace.core.WorkspaceBase;

public class StatusWorkspace extends WorkspaceBase {
    TextView mConnStatusTextView;
    @Override
    public String getWorkspaceName() {
        return "Status";
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.status_workspace, container, false);
        mConnStatusTextView = root.findViewById(R.id.connection_status);
        mConnStatusTextView.setText(AppContext.getApi(getContext()).getString("connection_status"));
        return root;
    }
    @Override
    public void activate() {
        System.out.println("activate called");
        mConnStatusTextView.setText(
                AppContext.getApi(getContext()).getString("connection_status"));
    }
}
