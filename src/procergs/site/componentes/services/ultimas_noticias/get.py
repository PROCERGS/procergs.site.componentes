from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.services import Service
from zope.component import getMultiAdapter


class UltimasNoticiasGet(Service):
    """endpoint customizado para exibir ultimas noticias"""

    def reply(self):
        catalog = self.context.portal_catalog
        request = self.request

        query = {
            "portal_type": "News Item",
        }

        b_start = int(request.form.get("b_start", 0))
        b_size = int(request.form.get("b_size", 10))

        sort_on = []

        indicador_manchete = request.form.get("manchete")
        indicador_destaque = request.form.get("destaque")

        # Prioritize 'manchete' first, then 'destaque', then 'effective'
        if indicador_manchete is not None and indicador_manchete.lower() in [
            "true",
            "1",
        ]:
            sort_on.append("indicador_manchete")

        if indicador_destaque is not None and indicador_destaque.lower() in [
            "true",
            "1",
        ]:
            sort_on.append("indicador_destaque")

        # Always sort by effective date last
        sort_on.append("effective")

        results = catalog(
            **query,
            sort_on=sort_on,
            sort_order="descending",
            b_size=b_size,
            b_start=b_start,
        )

        brains = [
            getMultiAdapter((brain, request), ISerializeToJsonSummary)()
            for brain in results
        ]

        return {
            "@id": self.context.absolute_url() + "/@ultimas_noticias",
            "items": brains,
            "items_total": catalog(
                **query, sort_on=sort_on, sort_order="descending"
            ).actual_result_count,
            "b_start": b_start,
            "b_size": b_size,
        }
