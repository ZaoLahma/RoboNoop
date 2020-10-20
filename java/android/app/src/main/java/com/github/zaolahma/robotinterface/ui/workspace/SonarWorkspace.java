package com.github.zaolahma.robotinterface.ui.workspace;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.constraintlayout.widget.ConstraintLayout;

import com.github.zaolahma.robotinterface.R;
import com.github.zaolahma.robotinterface.core.comm.MessageListener;
import com.github.zaolahma.robotinterface.core.comm.NetworkContext;
import com.github.zaolahma.robotinterface.core.comm.protocol.Message;
import com.github.zaolahma.robotinterface.core.comm.protocol.SonarDataMessage;
import com.github.zaolahma.robotinterface.ui.workspace.core.WorkspaceBase;

public class SonarWorkspace extends WorkspaceBase implements MessageListener {
    private static final int S_ROBOT_SIZE = 50;
    private static final double S_MAX_DISTANCE = 5000; //mm
    private static final int S_RADAR_SPOT_SIZE = 20;
    private double mCurrDistance = S_MAX_DISTANCE;
    private DrawableView mDrawableView;
    private boolean mActive = false;

    @Override
    public String getWorkspaceName() {
        return "Sonar";
    }

    @Override
    public void activate() {
        mActive = true;
    }

    @Override
    public void deactivate() {
        mActive = false;
    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.sonar_workspace, container, false);
        ConstraintLayout layout = (ConstraintLayout) root;
        mDrawableView = new DrawableView(getContext());
        layout.addView(mDrawableView);
        NetworkContext.getApi().addMessageListener(this);
        return root;
    }

    @Override
    public void handleMessage(Message message) {
        if (mActive && (message.getMessageId() == SonarDataMessage.MESSAGE_ID)) {
            SonarDataMessage sonarMessage = (SonarDataMessage) message;
            mCurrDistance = sonarMessage.getDistance();
            mDrawableView.invalidate();
        }
    }

    private class DrawableView extends View {
        public DrawableView(Context context) {
            super(context);
        }

        @Override
    public void onDraw(Canvas canvas) {
            canvas.drawColor(Color.rgb(0, 150, 150));
            Paint paint = new Paint();
            paint.setColor(Color.rgb(255, 0, 0));
            canvas.drawRect(canvas.getWidth() / 2 - S_ROBOT_SIZE, canvas.getHeight() - S_ROBOT_SIZE, canvas.getWidth() / 2 + S_ROBOT_SIZE, canvas.getHeight(), paint);

            paint.setColor(Color.rgb(0, 255, 0));
            double distanceFactor = mCurrDistance / S_MAX_DISTANCE;
            System.out.println("distanceFactor: " + distanceFactor);
            double relativeDistance = (canvas.getHeight()- S_ROBOT_SIZE) - (canvas.getHeight() - S_ROBOT_SIZE) * distanceFactor;
            System.out.println("relativeDistance: " + relativeDistance);
            canvas.drawCircle(canvas.getWidth() / 2, (int) (relativeDistance + 0.5), S_RADAR_SPOT_SIZE, paint);
        }
    }
}
