package br.com.barberagenda.controller;

import java.net.URI;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import br.com.barberagenda.dto.ClienteRequest;
import br.com.barberagenda.dto.ClienteResponse;
import br.com.barberagenda.model.Cliente;
import br.com.barberagenda.service.ClienteService;
import jakarta.validation.Valid;

/**
 * Cadastro de clientes (público). A listagem e a consulta por id expõem dados pessoais
 * e por isso exigem autenticação de administrador (ver SecurityConfig).
 */
@RestController
@RequestMapping("/api/clientes")
public class ClienteController {

    private final ClienteService clienteService;

    public ClienteController(ClienteService clienteService) {
        this.clienteService = clienteService;
    }

    @PostMapping
    public ResponseEntity<ClienteResponse> cadastrar(@Valid @RequestBody ClienteRequest dados) {
        Cliente cliente = clienteService.cadastrar(dados);
        URI local = ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}")
                .buildAndExpand(cliente.getId()).toUri();
        return ResponseEntity.created(local).body(ClienteResponse.de(cliente));
    }

    @GetMapping
    public List<ClienteResponse> listar() {
        return clienteService.listar().stream().map(ClienteResponse::de).toList();
    }

    @GetMapping("/{id}")
    public ClienteResponse buscar(@PathVariable Long id) {
        return ClienteResponse.de(clienteService.buscar(id));
    }
}
