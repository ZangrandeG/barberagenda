package br.com.barberagenda.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

import br.com.barberagenda.model.Agendamento;
import br.com.barberagenda.model.StatusAgendamento;

public record AgendamentoResponse(
        Long id,
        Long clienteId,
        String clienteNome,
        String clienteEmail,
        Long barbeiroId,
        String barbeiroNome,
        Long servicoId,
        String servicoNome,
        int duracaoMinutos,
        BigDecimal preco,
        LocalDateTime dataHoraInicio,
        LocalDateTime dataHoraFim,
        StatusAgendamento status,
        LocalDateTime dataCriacao) {

    public static AgendamentoResponse de(Agendamento a) {
        return new AgendamentoResponse(
                a.getId(),
                a.getCliente().getId(),
                a.getCliente().getNome(),
                a.getCliente().getEmail(),
                a.getBarbeiro().getId(),
                a.getBarbeiro().getNome(),
                a.getServico().getId(),
                a.getServico().getNome(),
                a.getServico().getDuracaoMinutos(),
                a.getServico().getPreco(),
                a.getDataHoraInicio(),
                a.getDataHoraFim(),
                a.getStatus(),
                a.getDataCriacao());
    }
}
