from gym.envs.registration import register

register(
    id='weightedrps-v1',
    entry_point='WeightedRPS.envs:WeightedRPSStandard',
)
register(
    id='weightedrpsinner-v1',
    entry_point='WeightedRPS.envs:WeightedRPSInner'
)
register(
    id='weightedrpsouter-v1',
    entry_point='WeightedRPS.envs:WeightedRPSOuter',
    kwargs={'agent': None,
            'full_step': None}
)
