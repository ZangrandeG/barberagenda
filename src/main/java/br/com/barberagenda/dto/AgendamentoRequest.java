package br.com.barberagenda.dto;

import java.time.LocalDateTime;
import java.util.Locale;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

/**
 * Pedido de agendamento feito pelo cliente. O cliente é identificado pelo e-mail cadastrado.
 * Formato de dataHoraInicio: "AAAA-MM-DDTHH:MM:SS" (horário local da barbearia).
 */
public record AgendamentoRequest(

        @NotBlank(message = "O e-mail do cliente é obrigatório.")
        @Email(message = "O e-mail informado é inválido.")
        String emailCliente,

        @NotNull(message = "O barbeiro é obrigatório.")
        Long barbeiroId,

        @NotNull(message = "O serviço é obrigatório.")
        Long servicoId,

        @NotNull(message = "A data e o horário são obrigatórios.")
        LocalDateTime dataHoraInicio) {

    public AgendamentoRequest {
        emailCliente = emailCliente == null ? null : emailCliente.strip().toLowerCase(Locale.ROOT);
    }
}
