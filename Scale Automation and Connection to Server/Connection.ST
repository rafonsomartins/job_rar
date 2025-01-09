CASE ciclo_estado OF

	// Initial state
	0: 
		IF NOT ciclo_iniciado THEN
			Connect := TRUE;
		END_IF;
		IF NOT ON_OFF[5] THEN
			ON_OFF[0] := TRUE;  // Trigger TCP connection
			ciclo_estado := 1;  // Move to the next state
		END_IF;

	// Wait for TCP connection to establish
	1: 
		IF NOT ON_OFF[0] THEN
			ON_OFF[4] := TRUE;
			ciclo_estado := 2; // Check connection Status
		END_IF;

	2:
		IF NOT ON_OFF[4] THEN
			ciclo_estado := 3;
		END_IF;

	//Wait for Status variable
	3:
		IF E4 OR Status <> _ESTABLISHED THEN
			ON_OFF[1] := TRUE;
			ciclo_estado := 99; // Connection Error
		ELSE
			IF NOT ON_OFF[4] THEN
				ON_OFF[4] := TRUE;
			END_IF;
			ciclo_estado := 2; // Keep checking the Connection Status
		END_IF;

	// Error handling state
	99: 
		IF NOT ON_OFF[1] THEN
				ON_OFF[5] := TRUE;
				ciclo_estado := 0; // Restart process
		END_IF;

END_CASE;
