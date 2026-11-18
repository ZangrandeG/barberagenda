package br.com.barberagenda.dto;

import br.com.barberagenda.model.Barbeiro;

public record BarbeiroResponse(Long id, String nome, boolean ativo) {

    public static BarbeiroResponse de(Barbeiro barbeiro) {
        return new BarbeiroResponse(barbeiro.getId(), barbeiro.getNome(), barbeiro.isAtivo());
    }
}
