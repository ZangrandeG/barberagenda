package br.com.barberagenda.dto;

import java.util.Locale;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

/** O cliente confirma a identidade informando o e-mail usado no agendamento. */
public record CancelamentoRequest(

        @NotBlank(message = "O e-mail é obrigatório.")
        @Email(message = "O e-mail informado é inválido.")
        String email) {

    public CancelamentoRequest {
        email = email == null ? null : email.strip().toLowerCase(Locale.ROOT);
    }
}
