package br.com.barberagenda.service;

import java.time.Clock;
import java.time.LocalDateTime;
import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import br.com.barberagenda.dto.ClienteRequest;
import br.com.barberagenda.exception.ConflitoException;
import br.com.barberagenda.exception.RecursoNaoEncontradoException;
import br.com.barberagenda.model.Cliente;
import br.com.barberagenda.repository.ClienteRepository;

@Service
public class ClienteService {

    private final ClienteRepository clienteRepository;
    private final Clock relogio;

    public ClienteService(ClienteRepository clienteRepository, Clock relogio) {
        this.clienteRepository = clienteRepository;
        this.relogio = relogio;
    }

    /** Cadastra um cliente. RN-03: o e-mail deve ser único (comparação sem diferenciar maiúsculas). */
    @Transactional
    public Cliente cadastrar(ClienteRequest dados) {
        if (clienteRepository.existsByEmailIgnoreCase(dados.email())) {
            throw new ConflitoException("Já existe um cliente cadastrado com este e-mail.");
        }
        Cliente cliente = new Cliente(dados.nome(), dados.telefone(), dados.email(), LocalDateTime.now(relogio));
        return clienteRepository.save(cliente);
    }

    @Transactional(readOnly = true)
    public List<Cliente> listar() {
        return clienteRepository.findAllByOrderByNomeAsc();
    }

    @Transactional(readOnly = true)
    public Cliente buscar(Long id) {
        return clienteRepository.findById(id)
                .orElseThrow(() -> new RecursoNaoEncontradoException("Cliente não encontrado."));
    }
}
