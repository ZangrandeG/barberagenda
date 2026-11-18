package br.com.barberagenda.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonInclude;

import br.com.barberagenda.model.Agendamento;
import br.com.barberagenda.model.StatusAgendamento;

/**
 * Dados do agendamento. O código de acesso só é enviado nas respostas ao próprio cliente
 * (agendar, consultar, cancelar); nas respostas administrativas ele é omitido.
 */
public record AgendamentoResponse(
        Long id,
        @JsonInclude(JsonInclude.Include.NON_NULL) String codigoAcesso,
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

    /** Resposta ao próprio cliente, com o código de acesso. */
    public static AgendamentoResponse paraCliente(Agendamento a) {
        return montar(a, a.getCodigoAcesso());
    }

    /** Resposta administrativa, sem o código de acesso. */
    public static AgendamentoResponse paraAdministrador(Agendamento a) {
        return montar(a, null);
    }

    private static AgendamentoResponse montar(Agendamento a, String codigoAcesso) {
        return new AgendamentoResponse(
                a.getId(),
                codigoAcesso,
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
