package br.com.barberagenda.dto;

import java.time.LocalDateTime;

import br.com.barberagenda.model.Cliente;

public record ClienteResponse(Long id, String nome, String telefone, String email, LocalDateTime dataCadastro) {

    public static ClienteResponse de(Cliente cliente) {
        return new ClienteResponse(cliente.getId(), cliente.getNome(), cliente.getTelefone(),
                cliente.getEmail(), cliente.getDataCadastro());
    }
}
