package br.com.barberagenda.dto;

import java.util.Locale;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

/** Dados de cadastro de cliente (RN-01, RN-02 e formato do RN-03). */
public record ClienteRequest(

        @NotBlank(message = "O nome é obrigatório.")
        @Size(min = 3, max = 60, message = "O nome deve ter entre 3 e 60 caracteres.")
        String nome,

        @NotBlank(message = "O telefone é obrigatório.")
        @Pattern(regexp = "\\d{10,11}", message = "O telefone deve conter somente dígitos, com 10 ou 11 dígitos (incluindo DDD).")
        String telefone,

        @NotBlank(message = "O e-mail é obrigatório.")
        @Size(max = 120, message = "O e-mail deve ter no máximo 120 caracteres.")
        @Email(regexp = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$", message = "O e-mail informado é inválido.")
        String email) {

    /** Remove espaços nas extremidades e padroniza o e-mail em minúsculas. */
    public ClienteRequest {
        nome = nome == null ? null : nome.strip();
        telefone = telefone == null ? null : telefone.strip();
        email = email == null ? null : email.strip().toLowerCase(Locale.ROOT);
    }
}
