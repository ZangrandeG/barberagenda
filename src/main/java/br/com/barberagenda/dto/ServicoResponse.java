package br.com.barberagenda.dto;

import java.math.BigDecimal;

import br.com.barberagenda.model.Servico;

public record ServicoResponse(Long id, String nome, int duracaoMinutos, BigDecimal preco, boolean ativo) {

    public static ServicoResponse de(Servico servico) {
        return new ServicoResponse(servico.getId(), servico.getNome(), servico.getDuracaoMinutos(),
                servico.getPreco(), servico.isAtivo());
    }
}
