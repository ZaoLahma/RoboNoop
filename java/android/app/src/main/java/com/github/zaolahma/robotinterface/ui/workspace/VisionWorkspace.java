package com.github.zaolahma.robotinterface.ui.workspace;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Bundle;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.constraintlayout.widget.ConstraintLayout;

import com.github.zaolahma.robotinterface.R;
import com.github.zaolahma.robotinterface.core.comm.MessageListener;
import com.github.zaolahma.robotinterface.core.comm.NetworkContext;
import com.github.zaolahma.robotinterface.core.comm.protocol.DataTransferMessage;
import com.github.zaolahma.robotinterface.core.comm.protocol.Message;
import com.github.zaolahma.robotinterface.ui.workspace.core.WorkspaceBase;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class VisionWorkspace extends WorkspaceBase implements MessageListener {
    private DrawableView mDrawableView;
    private boolean mActive = false;
    private byte[] mImageData;

    @Override
    public String getWorkspaceName() {
        return "Vision";
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
        if (mActive && (message.getMessageId() == DataTransferMessage.S_MESSAGE_ID)) {
            DataTransferMessage dataTransferMessage = (DataTransferMessage) message;

            mImageData = dataTransferMessage.getData();

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

            if (null != mImageData) {
                Paint paint = new Paint();
                int x = 0;
                int y = 0;
                int r = 0;
                int g = 0;
                int b = 0;
                for (int i = 0; i < mImageData.length; i += 3) {
                    r = mImageData[i];
                    g = mImageData[i + 1];
                    b = mImageData[i + 2];
                    paint.setColor(Color.rgb(r, g, b));
                    canvas.drawPoint(x, y, paint);
                    x++;
                    if (x == 640) {
                        x = 0;
                        y += 1;
                    }
                }
            }
        }
    }
}
