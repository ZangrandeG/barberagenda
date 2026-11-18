package br.com.barberagenda.controller;

import java.net.URI;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import br.com.barberagenda.dto.AgendamentoRequest;
import br.com.barberagenda.dto.AgendamentoResponse;
import br.com.barberagenda.dto.CancelamentoRequest;
import br.com.barberagenda.dto.HorariosDisponiveisResponse;
import br.com.barberagenda.model.Agendamento;
import br.com.barberagenda.service.AgendamentoService;
import jakarta.validation.Valid;

/** Operações públicas do cliente: horários livres, agendar, consultar e cancelar. */
@RestController
@RequestMapping("/api")
public class AgendamentoController {

    private static final DateTimeFormatter HORA = DateTimeFormatter.ofPattern("HH:mm");

    private final AgendamentoService agendamentoService;

    public AgendamentoController(AgendamentoService agendamentoService) {
        this.agendamentoService = agendamentoService;
    }

    @GetMapping("/horarios-disponiveis")
    public HorariosDisponiveisResponse horariosDisponiveis(
            @RequestParam Long barbeiroId,
            @RequestParam Long servicoId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate data) {
        var horarios = agendamentoService.horariosDisponiveis(barbeiroId, servicoId, data).stream()
                .map(inicio -> inicio.format(HORA))
                .toList();
        return new HorariosDisponiveisResponse(barbeiroId, servicoId, data, horarios);
    }

    @PostMapping("/agendamentos")
    public ResponseEntity<AgendamentoResponse> agendar(@Valid @RequestBody AgendamentoRequest pedido) {
        Agendamento agendamento = agendamentoService.agendar(pedido);
        URI local = ServletUriComponentsBuilder.fromCurrentRequest().path("/{codigo}")
                .buildAndExpand(agendamento.getCodigoAcesso()).toUri();
        return ResponseEntity.created(local).body(AgendamentoResponse.paraCliente(agendamento));
    }

    /** Consulta pelo cliente: código de acesso recebido no agendamento + e-mail do cliente. */
    @GetMapping("/agendamentos/{codigoAcesso}")
    public AgendamentoResponse consultar(@PathVariable String codigoAcesso, @RequestParam String email) {
        return AgendamentoResponse.paraCliente(agendamentoService.consultarPeloCliente(codigoAcesso, email));
    }

    @PatchMapping("/agendamentos/{codigoAcesso}/cancelar")
    public AgendamentoResponse cancelar(@PathVariable String codigoAcesso,
                                        @Valid @RequestBody CancelamentoRequest dados) {
        return AgendamentoResponse.paraCliente(agendamentoService.cancelarPeloCliente(codigoAcesso, dados.email()));
    }
}
