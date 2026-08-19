export type AvailableConnector = {
  code: string;
  name: string;
};

export const AVAILABLE_CONNECTORS: AvailableConnector[] = [
  {
    code: "france_travail",
    name: "France Travail",
  },
  {
    code: "greenhouse",
    name: "Greenhouse",
  },
  {
    code: "linkedin",
    name: "LinkedIn",
  },
];

export function getConnectorLabel(
  connectorCode: string,
): string {
  const connector =
    AVAILABLE_CONNECTORS.find(
      (item) => item.code === connectorCode,
    );

  if (!connector) {
    return connectorCode;
  }

  return connector.name;
}