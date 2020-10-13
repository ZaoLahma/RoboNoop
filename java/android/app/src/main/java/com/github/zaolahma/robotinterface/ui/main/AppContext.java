package com.github.zaolahma.robotinterface.ui.main;

import android.content.Context;
import android.os.Bundle;

import com.github.zaolahma.robotinterface.R;

import org.w3c.dom.Attr;

public class AppContext {
    private static AppContext S_INSTANCE = null;

    private Bundle mBundle;
    private Context mContext;

    private AppContext(Context context) {
        mContext = context;
        mBundle = new Bundle();

        String[] baseAttrs = mContext.getResources().getStringArray(R.array.base_attrs);
        String[] baseAttrTypes = mContext.getResources().getStringArray(R.array.base_attrs_types);
        String[] baseAttrValues = mContext.getResources().getStringArray(R.array.base_attrs_values);

        for (int i = 0; i < baseAttrs.length; ++i) {
            String type = baseAttrTypes[i];
            if ("String".equals(type)) {
                mBundle.putString(baseAttrs[i], baseAttrValues[i]);
            }
        }
    }

    public static AppContext getApi(Context context) {
        if (null == S_INSTANCE) {
            S_INSTANCE = new AppContext(context.getApplicationContext());
        }

        return S_INSTANCE;
    }

    public void setBoolean(String attrName, boolean value) {
        mBundle.putBoolean(attrName, value);
    }

    public Boolean getBoolean(String attrName) {
        Object attr = mBundle.get(attrName);
        if (null != attr && attr instanceof Boolean) {
            return (Boolean) attr;
        }
        return null;
    }

    public void setString(String attrName, String value) {
        mBundle.putString(attrName, value);
    }

    public String getString(String attrName) {
        Object attr = mBundle.get(attrName);
        if (null != attr && attr instanceof String) {
            return (String) attr;
        }
        return null;
    }
}
