package br.com.barberagenda.dto;

import java.math.BigDecimal;

import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Digits;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

/** Dados de cadastro/edição de serviço (RN-09). Se "ativo" não for informado, assume verdadeiro. */
public record ServicoRequest(

        @NotBlank(message = "O nome é obrigatório.")
        @Size(min = 3, max = 60, message = "O nome deve ter entre 3 e 60 caracteres.")
        String nome,

        @NotNull(message = "A duração é obrigatória.")
        @Min(value = 15, message = "A duração deve ser de no mínimo 15 minutos.")
        @Max(value = 180, message = "A duração deve ser de no máximo 180 minutos.")
        @MultiploDe(valor = 15, message = "A duração deve ser múltipla de 15 minutos.")
        Integer duracaoMinutos,

        @NotNull(message = "O preço é obrigatório.")
        @DecimalMin(value = "1.00", message = "O preço deve ser de no mínimo R$ 1,00.")
        @DecimalMax(value = "1000.00", message = "O preço deve ser de no máximo R$ 1.000,00.")
        @Digits(integer = 4, fraction = 2, message = "O preço deve ter no máximo 2 casas decimais.")
        BigDecimal preco,

        Boolean ativo) {

    public ServicoRequest {
        nome = nome == null ? null : nome.strip();
    }

    public boolean ativoOuPadrao() {
        return ativo == null || ativo;
    }
}
