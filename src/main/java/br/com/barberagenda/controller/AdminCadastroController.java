package br.com.barberagenda.controller;

import java.net.URI;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import br.com.barberagenda.dto.BarbeiroRequest;
import br.com.barberagenda.dto.BarbeiroResponse;
import br.com.barberagenda.dto.ServicoRequest;
import br.com.barberagenda.dto.ServicoResponse;
import br.com.barberagenda.model.Barbeiro;
import br.com.barberagenda.model.Servico;
import br.com.barberagenda.service.BarbeiroService;
import br.com.barberagenda.service.ServicoService;
import jakarta.validation.Valid;

/** Cadastro de barbeiros e serviços (somente administrador — RN-11). */
@RestController
@RequestMapping("/api/admin")
public class AdminCadastroController {

    private final BarbeiroService barbeiroService;
    private final ServicoService servicoService;

    public AdminCadastroController(BarbeiroService barbeiroService, ServicoService servicoService) {
        this.barbeiroService = barbeiroService;
        this.servicoService = servicoService;
    }

    // ---------- Barbeiros ----------

    @GetMapping("/barbeiros")
    public List<BarbeiroResponse> listarBarbeiros() {
        return barbeiroService.listarTodos().stream().map(BarbeiroResponse::de).toList();
    }

    @PostMapping("/barbeiros")
    public ResponseEntity<BarbeiroResponse> cadastrarBarbeiro(@Valid @RequestBody BarbeiroRequest dados) {
        Barbeiro barbeiro = barbeiroService.cadastrar(dados);
        return ResponseEntity.created(local(barbeiro.getId())).body(BarbeiroResponse.de(barbeiro));
    }

    @PutMapping("/barbeiros/{id}")
    public BarbeiroResponse atualizarBarbeiro(@PathVariable Long id, @Valid @RequestBody BarbeiroRequest dados) {
        return BarbeiroResponse.de(barbeiroService.atualizar(id, dados));
    }

    @DeleteMapping("/barbeiros/{id}")
    public ResponseEntity<Void> excluirBarbeiro(@PathVariable Long id) {
        barbeiroService.excluir(id);
        return ResponseEntity.noContent().build();
    }

    // ---------- Serviços ----------

    @GetMapping("/servicos")
    public List<ServicoResponse> listarServicos() {
        return servicoService.listarTodos().stream().map(ServicoResponse::de).toList();
    }

    @PostMapping("/servicos")
    public ResponseEntity<ServicoResponse> cadastrarServico(@Valid @RequestBody ServicoRequest dados) {
        Servico servico = servicoService.cadastrar(dados);
        return ResponseEntity.created(local(servico.getId())).body(ServicoResponse.de(servico));
    }

    @PutMapping("/servicos/{id}")
    public ServicoResponse atualizarServico(@PathVariable Long id, @Valid @RequestBody ServicoRequest dados) {
        return ServicoResponse.de(servicoService.atualizar(id, dados));
    }

    @DeleteMapping("/servicos/{id}")
    public ResponseEntity<Void> excluirServico(@PathVariable Long id) {
        servicoService.excluir(id);
        return ResponseEntity.noContent().build();
    }

    private static URI local(Long id) {
        return ServletUriComponentsBuilder.fromCurrentRequest().path("/{id}").buildAndExpand(id).toUri();
    }
}
