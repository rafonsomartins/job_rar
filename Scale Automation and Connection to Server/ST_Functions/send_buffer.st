FOR i := 1 TO buffer_index DO
    send_to_server(buffer_peso[i], buffer_time[i]);
END_FOR;
i := 0;

buffer_index := 0;
send_buffer := TRUE;
