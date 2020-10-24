package com.github.zaolahma.robotinterface;

import android.content.Context;
import android.content.pm.ActivityInfo;
import android.hardware.SensorManager;
import android.os.Bundle;

import com.github.zaolahma.robotinterface.core.comm.NetworkContext;
import com.github.zaolahma.robotinterface.ui.workspace.RemoteControlWorkspace;
import com.github.zaolahma.robotinterface.ui.workspace.SonarWorkspace;
import com.github.zaolahma.robotinterface.ui.workspace.StatusWorkspace;
import com.google.android.material.tabs.TabLayout;

import androidx.viewpager.widget.ViewPager;
import androidx.appcompat.app.AppCompatActivity;

import com.github.zaolahma.robotinterface.ui.workspace.core.WorkspaceManager;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        /*
        Don't rotate please
         */
        setRequestedOrientation (ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        setContentView(R.layout.activity_main);
        final WorkspaceManager workspaceManager = new WorkspaceManager(this, getSupportFragmentManager());
        workspaceManager.addWorkspace(new StatusWorkspace());
        workspaceManager.addWorkspace(new SonarWorkspace());
        workspaceManager.addWorkspace(new RemoteControlWorkspace((SensorManager) getSystemService(Context.SENSOR_SERVICE)));
        ViewPager viewPager = findViewById(R.id.view_pager);
        viewPager.setAdapter(workspaceManager);
        TabLayout tabs = findViewById(R.id.tabs);
        tabs.setupWithViewPager(viewPager);

        tabs.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {

            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                workspaceManager.onPageSelected(tab.getPosition());
            }

            @Override
            public void onTabUnselected(TabLayout.Tab tab) {
            }

            @Override
            public void onTabReselected(TabLayout.Tab tab) {
            }
        });
    }

    @Override
    protected void onStop() {
        super.onStop();
        NetworkContext.getApi().disconnect();
    }
}