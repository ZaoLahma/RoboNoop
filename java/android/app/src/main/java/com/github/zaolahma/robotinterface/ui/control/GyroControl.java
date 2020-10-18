package com.github.zaolahma.robotinterface.ui.control;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

public class GyroControl implements SensorEventListener {
    private static float S_SENSOR_TO_ANGLE_FACTOR = 9f;

    private double mPitchAngle;
    private double mRollAngle;

    public GyroControl(SensorManager sensorManager) {
        sensorManager.registerListener(this, sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), SensorManager.SENSOR_DELAY_GAME);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            mPitchAngle = (double) (S_SENSOR_TO_ANGLE_FACTOR * -event.values[1]);
            mRollAngle = (double) (S_SENSOR_TO_ANGLE_FACTOR * event.values[0]);
        }
    }

    public double getPitchAngle() {
        return mPitchAngle;
    }

    public double getRollAngle() {
        return mRollAngle;
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
}
