package br.com.barberagenda.repository;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import br.com.barberagenda.model.Agendamento;
import br.com.barberagenda.model.StatusAgendamento;

public interface AgendamentoRepository extends JpaRepository<Agendamento, Long> {

    long countByClienteIdAndStatus(Long clienteId, StatusAgendamento status);

    boolean existsByBarbeiroId(Long barbeiroId);

    boolean existsByServicoId(Long servicoId);

    /** Verifica se existe agendamento ativo do barbeiro que se sobreponha ao intervalo [inicio, fim). */
    @Query("""
            select count(a) > 0 from Agendamento a
            where a.barbeiro.id = :barbeiroId
              and a.status = br.com.barberagenda.model.StatusAgendamento.AGENDADO
              and a.dataHoraInicio < :fim
              and a.dataHoraFim > :inicio
            """)
    boolean existeSobreposicao(@Param("barbeiroId") Long barbeiroId,
                               @Param("inicio") LocalDateTime inicio,
                               @Param("fim") LocalDateTime fim);

    /** Agendamentos do barbeiro (qualquer status) que começam no intervalo [inicio, fim). */
    @Query("""
            select a from Agendamento a
            where a.barbeiro.id = :barbeiroId
              and a.dataHoraInicio >= :inicio
              and a.dataHoraInicio < :fim
            order by a.dataHoraInicio
            """)
    List<Agendamento> buscarDoBarbeiroNoPeriodo(@Param("barbeiroId") Long barbeiroId,
                                                @Param("inicio") LocalDateTime inicio,
                                                @Param("fim") LocalDateTime fim);
}
