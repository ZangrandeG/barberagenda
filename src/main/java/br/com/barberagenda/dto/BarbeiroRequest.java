package br.com.barberagenda.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** Dados de cadastro/edição de barbeiro. Se "ativo" não for informado, assume verdadeiro. */
public record BarbeiroRequest(

        @NotBlank(message = "O nome é obrigatório.")
        @Size(min = 3, max = 60, message = "O nome deve ter entre 3 e 60 caracteres.")
        String nome,

        Boolean ativo) {

    public BarbeiroRequest {
        nome = nome == null ? null : nome.strip();
    }

    public boolean ativoOuPadrao() {
        return ativo == null || ativo;
    }
}
