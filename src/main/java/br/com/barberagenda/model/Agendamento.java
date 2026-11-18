package br.com.barberagenda.model;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "agendamento")
public class Agendamento {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** Código aleatório entregue ao cliente; exigido (com o e-mail) para consultar e cancelar. */
    @Column(name = "codigo_acesso", nullable = false, length = 8, unique = true)
    private String codigoAcesso;

    @ManyToOne(optional = false)
    @JoinColumn(name = "cliente_id", nullable = false)
    private Cliente cliente;

    @ManyToOne(optional = false)
    @JoinColumn(name = "barbeiro_id", nullable = false)
    private Barbeiro barbeiro;

    @ManyToOne(optional = false)
    @JoinColumn(name = "servico_id", nullable = false)
    private Servico servico;

    @Column(name = "data_hora_inicio", nullable = false)
    private LocalDateTime dataHoraInicio;

    /** Calculada a partir do início e da duração do serviço. */
    @Column(name = "data_hora_fim", nullable = false)
    private LocalDateTime dataHoraFim;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private StatusAgendamento status;

    @Column(name = "data_criacao", nullable = false)
    private LocalDateTime dataCriacao;

    protected Agendamento() {
        // exigido pela JPA
    }

    public Agendamento(String codigoAcesso, Cliente cliente, Barbeiro barbeiro, Servico servico,
                       LocalDateTime dataHoraInicio, StatusAgendamento status, LocalDateTime dataCriacao) {
        this.codigoAcesso = codigoAcesso;
        this.cliente = cliente;
        this.barbeiro = barbeiro;
        this.servico = servico;
        this.dataHoraInicio = dataHoraInicio;
        this.dataHoraFim = dataHoraInicio.plusMinutes(servico.getDuracaoMinutos());
        this.status = status;
        this.dataCriacao = dataCriacao;
    }

    public void cancelar() {
        this.status = StatusAgendamento.CANCELADO;
    }

    public void concluir() {
        this.status = StatusAgendamento.CONCLUIDO;
    }

    public boolean isAgendado() {
        return status == StatusAgendamento.AGENDADO;
    }

    public Long getId() {
        return id;
    }

    public String getCodigoAcesso() {
        return codigoAcesso;
    }

    public Cliente getCliente() {
        return cliente;
    }

    public Barbeiro getBarbeiro() {
        return barbeiro;
    }

    public Servico getServico() {
        return servico;
    }

    public LocalDateTime getDataHoraInicio() {
        return dataHoraInicio;
    }

    public LocalDateTime getDataHoraFim() {
        return dataHoraFim;
    }

    public StatusAgendamento getStatus() {
        return status;
    }

    public LocalDateTime getDataCriacao() {
        return dataCriacao;
    }
}
