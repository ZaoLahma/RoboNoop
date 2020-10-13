package com.github.zaolahma.robotinterface.ui.main;

import android.content.Context;

import androidx.annotation.Nullable;
import androidx.annotation.StringRes;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;

import com.github.zaolahma.robotinterface.R;

import java.util.ArrayList;
import java.util.List;

/**
 * A [FragmentPagerAdapter] that returns a fragment corresponding to
 * one of the sections/tabs/pages.
 */
public class WorkspaceManager extends FragmentPagerAdapter {

    private List<WorkspaceBase> mWorkspaces;
    private final Context mContext;

    public WorkspaceManager(Context context, FragmentManager fm) {
        super(fm);
        mWorkspaces = new ArrayList<WorkspaceBase>();
        mContext = context;
    }

    public void addWorkspace(WorkspaceBase workspace) {
        mWorkspaces.add(workspace);
    }

    @Override
    public Fragment getItem(int position) {
        return mWorkspaces.get(position);
    }

    @Nullable
    @Override
    public CharSequence getPageTitle(int position) {
        WorkspaceBase ws = mWorkspaces.get(position);
        return ws.getWorkspaceName();
    }

    @Override
    public int getCount() {
        return mWorkspaces.size();
    }
}