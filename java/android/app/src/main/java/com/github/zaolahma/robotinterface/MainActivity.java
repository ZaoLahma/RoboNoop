package com.github.zaolahma.robotinterface;

import android.os.Bundle;

import com.github.zaolahma.robotinterface.ui.main.NetworkWorkspace;
import com.github.zaolahma.robotinterface.ui.main.StatusWorkspace;
import com.google.android.material.tabs.TabLayout;

import androidx.viewpager.widget.ViewPager;
import androidx.appcompat.app.AppCompatActivity;

import com.github.zaolahma.robotinterface.ui.main.WorkspaceManager;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        WorkspaceManager workspaceManager = new WorkspaceManager(this, getSupportFragmentManager());
        workspaceManager.addWorkspace(new StatusWorkspace());
        workspaceManager.addWorkspace(new NetworkWorkspace());
        ViewPager viewPager = findViewById(R.id.view_pager);
        viewPager.setAdapter(workspaceManager);
        TabLayout tabs = findViewById(R.id.tabs);
        tabs.setupWithViewPager(viewPager);
    }
}