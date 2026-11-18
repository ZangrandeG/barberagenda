package br.com.barberagenda.controller;

import java.security.Principal;
import java.time.LocalDate;
import java.util.List;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import br.com.barberagenda.dto.AgendamentoResponse;
import br.com.barberagenda.dto.SessaoResponse;
import br.com.barberagenda.service.AgendamentoService;

/** Agenda do dia e conclusão de atendimentos (somente administrador — RN-11). */
@RestController
@RequestMapping("/api/admin")
public class AdminAgendaController {

    private final AgendamentoService agendamentoService;

    public AdminAgendaController(AgendamentoService agendamentoService) {
        this.agendamentoService = agendamentoService;
    }

    @GetMapping("/agenda")
    public List<AgendamentoResponse> agendaDoDia(
            @RequestParam Long barbeiroId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate data) {
        return agendamentoService.agendaDoDia(barbeiroId, data).stream()
                .map(AgendamentoResponse::paraAdministrador)
                .toList();
    }

    @PatchMapping("/agendamentos/{id}/concluir")
    public AgendamentoResponse concluir(@PathVariable Long id) {
        return AgendamentoResponse.paraAdministrador(agendamentoService.concluir(id));
    }

    /** Usado pelas páginas administrativas para exibir o usuário autenticado. */
    @GetMapping("/sessao")
    public SessaoResponse sessao(Principal usuario) {
        return new SessaoResponse(usuario.getName());
    }
}
