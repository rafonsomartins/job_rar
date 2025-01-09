peso_str := INT_TO_STRING(peso);
timestamp_str := UDINT_TO_STRING(timestamp);
message := CONCAT(CONCAT(peso_str, ';'), timestamp_str);
data_size := LEN(message);
StringToAry(message, Data[0]);

IF NOT E4 AND Status = _ESTABLISHED THEN
	ON_OFF[2] := TRUE;
END_IF;

IF NOT ON_OFF[2] THEN
	send_to_server := TRUE;
END_IF;
