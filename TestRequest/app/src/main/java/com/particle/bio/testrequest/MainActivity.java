package com.particle.bio.testrequest;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.ScrollingMovementMethod;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;



public class MainActivity extends AppCompatActivity {

    Button button;
    TextView textView;
    String server_url = "https://temperatureapi-developer-edition.na40.force.com/services/apexrest/Temperatures";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        button = (Button)findViewById(R.id.bn);
        textView = (TextView)findViewById(R.id.txt);
        textView.setMovementMethod(new ScrollingMovementMethod());

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                //Add New temperature in this JSONobject
                JSONObject body = new JSONObject();

                try {
                    body.put("Name", "test temp 2");
                } catch (JSONException e) {
                    e.printStackTrace();
                }

                final RequestQueue requestQueue = Volley.newRequestQueue(MainActivity.this);

                //When using POST, add "body" parameter to send JSON
                JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(Request.Method.GET,server_url,
                        new Response.Listener<JSONArray>() {
                            @Override
                            public void onResponse(JSONArray response) {

                                int count = 0;
                                while (count < response.length()) {
                                    try {
                                        JSONObject jsonObject = response.getJSONObject(count);
                                        String temperature = jsonObject.getString("Name");
                                        textView.append(temperature + " °C" + "\n");
                                        count++;
                                    } catch (JSONException e){
                                        e.printStackTrace();
                                    }
                                }

                                requestQueue.stop();

                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                        textView.setText("Something went wrong...");
                        error.printStackTrace();
                        requestQueue.stop();
                    }
                });

                requestQueue.add(jsonArrayRequest);
            }
        });
    }



}
