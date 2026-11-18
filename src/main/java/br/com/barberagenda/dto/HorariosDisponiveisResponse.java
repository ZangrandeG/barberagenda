package br.com.barberagenda.dto;

import java.time.LocalDate;
import java.util.List;

/** Horários de início livres (formato HH:MM) para o barbeiro e o serviço na data informada. */
public record HorariosDisponiveisResponse(Long barbeiroId, Long servicoId, LocalDate data, List<String> horarios) {
}
