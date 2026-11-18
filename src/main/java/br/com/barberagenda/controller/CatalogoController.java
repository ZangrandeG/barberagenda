package br.com.barberagenda.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import br.com.barberagenda.dto.BarbeiroResponse;
import br.com.barberagenda.dto.ServicoResponse;
import br.com.barberagenda.service.BarbeiroService;
import br.com.barberagenda.service.ServicoService;

/** Consultas públicas usadas no agendamento: somente barbeiros e serviços ativos. */
@RestController
@RequestMapping("/api")
public class CatalogoController {

    private final BarbeiroService barbeiroService;
    private final ServicoService servicoService;

    public CatalogoController(BarbeiroService barbeiroService, ServicoService servicoService) {
        this.barbeiroService = barbeiroService;
        this.servicoService = servicoService;
    }

    @GetMapping("/barbeiros")
    public List<BarbeiroResponse> barbeirosAtivos() {
        return barbeiroService.listarAtivos().stream().map(BarbeiroResponse::de).toList();
    }

    @GetMapping("/servicos")
    public List<ServicoResponse> servicosAtivos() {
        return servicoService.listarAtivos().stream().map(ServicoResponse::de).toList();
    }
}
