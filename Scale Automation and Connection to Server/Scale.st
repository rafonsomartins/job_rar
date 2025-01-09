IF ciclo_iniciado = 0 THEN
	ciclo_iniciado := 1;
	IF NOT closed_inf_temp THEN
		cilindro_inf := FALSE;
	END_IF;
	IF closed_sup_temp THEN
		cilindro_sup := TRUE;
	END_IF;
	ciclo_iniciado := 1;
END_IF;

CASE ciclo OF

	0:
		IF leitura_balanca >= 180 THEN
			cilindro_sup := FALSE;
			IF closed_sup_temp THEN
				(* Stabilization Timer *)
				First_Timer(In:=TRUE, PT:=tempo_estabilizacao, Q=>FOut);
				IF FOut THEN
					peso_inicial := leitura_balanca;

					(* Open Bottom Cylinder *)
					cilindro_inf := TRUE;
					Second_Timer(In:=TRUE, PT:=tempo_abertura, Q=>SOut);
					IF SOut THEN
						ciclo := 1;
					END_IF;
				END_IF;
			END_IF;
		END_IF;

	1:
			cilindro_inf := FALSE;

			IF closed_inf_temp THEN
				Third_Timer(In:=TRUE, PT:=tempo_estabilizacao, Q=>TOut);

				IF TOut THEN
					peso_final := leitura_balanca;
					peso_rama := peso_inicial - peso_final;
					timestamp := GetTime();

					IF NOT E4 AND Status = _ESTABLISHED THEN
						IF buffer_index > 0 THEN
							send_buffer();
						END_IF;

						send_to_server(REAL_TO_UINT((peso_rama * 10)), LINT_TO_UDINT(DtToSec(timestamp)));
					ELSE
						buffer_index := buffer_index + 1;
						IF buffer_index > MAX_BUFFER THEN
							buffer_index := 1; // Circular buffer
						END_IF;

						buffer_peso[buffer_index] := REAL_TO_UINT((peso_rama * 10));
						buffer_time[buffer_index] := LINT_TO_UDINT(DtToSec(timestamp));
					END_IF;
					First_Timer(In:=False, Q=>FOut);
					Second_Timer(In:=False, Q=>SOut);
					Third_Timer(In:=False, Q=>TOut);
					ciclo := 2;
				END_IF;
			END_IF;

	2:
		cilindro_sup := TRUE;
		IF NOT closed_sup_temp THEN
			ciclo := 0;
		END_IF;
		
END_CASE;
